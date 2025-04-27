import pandas as pd
import numpy as np
import joblib
import os
import glob
from datetime import datetime # To handle datetime input
import gc # Import the garbage collector module
import time # To potentially add delays if needed
# Make sure xgboost and lightgbm are installed if you might load models from either
# import xgboost as xgb
# import lightgbm as lgb
from . import utils
# import traind_models

def clean_label(label):
    """
    Removes standard prefixes/suffixes ('has_', '_next_24h_here')
    and replaces underscores with spaces for better readability.


    Args:
        label (str): The original target column name.


    Returns:
        str: The cleaned label.
    """
    if isinstance(label, str): # Ensure input is a string
        label = label.replace('has_', '')
        label = label.replace('_next_24h_here', '')
        label = label.replace('_', ' ') # Replace underscores with spaces
    return label


# Defaulting to the latest XGBoost models directory, change if needed
def predict_next_event_probabilities(event_data, models_directory='trained_models', datetime_col='תאריך ושעה פתיחה'):
    """
    Predicts the probability of various 'next event' types occurring within 24 hours,
    based on the input event data, using previously trained models.
    Optimized for lower memory usage with enhanced logging.
    *** IMPORTANT: Assumes models were trained using the feature engineering
        from the LightGBM/XGBoost training scripts (cyclical time, weekend flag) ***


    Args:
        event_data (dict): A dictionary representing a single event.
                           Must contain all *raw* features required by the
                           feature engineering steps (latitude, longitude, temp, etc.)
                           including the original datetime column specified by `datetime_col`.
        models_directory (str): Path to the directory containing the saved
                                scikit-learn pipeline (.joblib) files.
                                *** Ensure this points to the correct directory
                                    (e.g., 'trained_models' or 'trained_models_lgbm_v1') ***
        datetime_col (str): The name of the key in `event_data` that holds
                            the primary datetime information for the event.


    Returns:
        dict: A dictionary mapping cleaned event type names (str) to their
              predicted probabilities (float, between 0.0 and 1.0). Sorted.
              Returns an empty dictionary if no models are found or critical errors occur.
    """
    print("--- Starting Prediction Function ---")
    if gc.isenabled(): print("Garbage collector is enabled.")
    else: gc.enable(); print("Garbage collector enabled.")


    # --- 1. Find Saved Model Pipeline Files ---
    print(f"Searching for models in: {os.path.abspath(models_directory)}")
    model_files = glob.glob(os.path.join(models_directory, 'pipeline_*.joblib'))
    if not model_files:
        print(f"Error: No model pipeline files ('pipeline_*.joblib') found in '{models_directory}'.")
        print("--- Prediction Function Ended (No Models Found) ---")
        return {}
    print(f"Found {len(model_files)} model pipelines.")
    predictions = {}


    # --- 2. Prepare Input Data ONCE (with matching Feature Engineering) ---
    print("Preparing input data...")
    try:
        input_df = pd.DataFrame([event_data])


        # --- Datetime Conversion ---
        if datetime_col not in input_df.columns:
            raise ValueError(f"Input 'event_data' missing datetime column '{datetime_col}'.")
        input_df[datetime_col] = pd.to_datetime(input_df[datetime_col], errors='coerce')
        if input_df[datetime_col].isnull().any():
             raise ValueError(f"Invalid datetime value in '{datetime_col}'.")


        # --- Feature Engineering (Matching Training Script) ---
        # Basic time features (needed for engineering)
        input_df['event_hour'] = input_df[datetime_col].dt.hour
        input_df['event_dayofweek'] = input_df[datetime_col].dt.dayofweek # Mon=0, Sun=6
        input_df['event_month'] = input_df[datetime_col].dt.month


        # Cyclical Hour Features
        input_df['hour_sin'] = np.sin(2 * np.pi * input_df['event_hour']/24.0)
        input_df['hour_cos'] = np.cos(2 * np.pi * input_df['event_hour']/24.0)


        # Cyclical Day of Week Features
        input_df['dayofweek_sin'] = np.sin(2 * np.pi * input_df['event_dayofweek']/7.0)
        input_df['dayofweek_cos'] = np.cos(2 * np.pi * input_df['event_dayofweek']/7.0)


        # Weekend Feature (Assuming Friday=4, Saturday=5 are weekend)
        input_df['is_weekend'] = input_df['event_dayofweek'].isin([4, 5]).astype(int)
        # ------------------------------------------------------
        print("Engineered features created (cyclical time, weekend).")
        print(f"Input DataFrame shape after engineering: {input_df.shape}")
        # The pipeline's preprocessor expects specific columns used during training.
        # We created them above. The 'remainder=drop' in the preprocessor handles selection.
        # print(f"Columns available for pipeline: {input_df.columns.tolist()}") # For debugging


    except KeyError as e:
        print(f"Error preparing input data: Missing expected raw key {e} in 'event_data'.")
        # List raw features required by the feature engineering logic
        print(f"Required raw features: latitude, longitude, Maximum Temperature (°C), Gale, נושא, חג_עברי, {datetime_col}")
        print("--- Prediction Function Ended (Input Error) ---")
        return {}
    except ValueError as e:
         print(f"Error preparing input data: {e}")
         print("--- Prediction Function Ended (Input Error) ---")
         return {}
    except Exception as e:
        print(f"An unexpected error occurred preparing input data: {type(e).__name__}: {e}")
        print("--- Prediction Function Ended (Input Error) ---")
        return {}


    # --- 3. Loop Through Models: Load -> Predict -> Delete -> Collect Garbage ---
    print(f"\n--- Starting Loop Through {len(model_files)} Models ---")
    for i, model_path in enumerate(model_files):
        target_col_raw = None
        model_pipeline = None
        print(f"\nProcessing model {i+1}/{len(model_files)}: {os.path.basename(model_path)}", flush=True)
        try:
            filename = os.path.basename(model_path)
            if not filename.startswith('pipeline_') or not filename.endswith('.joblib'):
                print(f"Warning: Skipping file with unexpected name format: {filename}", flush=True)
                continue
            target_col_raw = filename.replace('pipeline_', '', 1).replace('.joblib', '')
            print(f"  Target: {target_col_raw}", flush=True)


            # Load model
            print(f"  Loading model...", flush=True); start_load_time = time.time()
            model_pipeline = joblib.load(model_path)
            load_time = time.time() - start_load_time; print(f"  Model loaded. ({load_time:.2f}s)", flush=True)


            # Predict probability
            print(f"  Predicting probability...", flush=True); start_pred_time = time.time()
            # Pass the DataFrame with *all* engineered features. The pipeline's
            # ColumnTransformer ('preprocessor' step) will select the ones it needs.
            probability_positive_class = model_pipeline.predict_proba(input_df)[0, 1]
            pred_time = time.time() - start_pred_time; print(f"  Prediction complete. Prob={probability_positive_class:.4f} ({pred_time:.2f}s)", flush=True)


            cleaned_event_name = clean_label(target_col_raw)
            predictions[cleaned_event_name] = probability_positive_class


        # Error Handling
        except FileNotFoundError: print(f"  ERROR: Model file not found {model_path}.", flush=True)
        except (joblib.externals.loky.process_executor.TerminatedWorkerError, EOFError): print(f"  ERROR: Joblib worker terminated/EOFError for '{target_col_raw}'. Check memory/file.", flush=True)

        except KeyError as e: print(f"  ERROR predicting for '{target_col_raw}': Required feature {e} not found by pipeline's preprocessor.", flush=True)
        except ValueError as e: print(f"  ERROR during prediction for '{target_col_raw}': {e}.", flush=True)
        except Exception as e: target_name = target_col_raw or os.path.basename(model_path); print(f"  UNEXPECTED ERROR for '{target_name}': {type(e).__name__}: {e}", flush=True)
        finally:
            # Clean up
            if model_pipeline is not None: del model_pipeline; # print(f"  Model object deleted.", flush=True)
            # else: print(f"  Model object None.", flush=True)
            collected_count = gc.collect(); # print(f"  GC collected {collected_count} objects.", flush=True)




    # --- 4. Sort Results ---
    print("\n--- Model Loop Finished ---")
    print(f"Successfully processed {len(predictions)} models out of {len(model_files)} found.")
    if not predictions:
        print("Warning: No predictions generated."); print("--- Prediction Function Ended (No Results) ---"); return {}


    print("Sorting results...")
    sorted_predictions = dict(sorted(predictions.items(), key=lambda item: item[1], reverse=True))
    print("Prediction process complete."); print("--- Prediction Function Ended Successfully ---")
    return sorted_predictions


# ===============================================================
# --- Example Usage (Updated for Latest Features & Model Dir) ---
# ===============================================================


# 1. Define a COMPLETE sample event dictionary with RAW features
def predict(sample_event, path):
    # 2. Define the directory where the **XGBoost** (or LightGBM) models are saved
    #    *** UPDATE THIS PATH IF NECESSARY ***
    MODELS_SAVE_DIRECTORY = path  # <<< Ensure this is correct



    # 3. Call the prediction function
    print("Calling predict_next_event_probabilities...")
    event_probabilities = predict_next_event_probabilities(
        event_data=sample_event,
        models_directory=MODELS_SAVE_DIRECTORY,
        datetime_col='תאריך ושעה פתיחה'
    )
    print("Function call returned.")


# 4. Print the results
    if event_probabilities:
        print("\nPredicted Probabilities for Next Event Types (Sorted):")
        for event_type, probability in event_probabilities.items():
            print(f"- {event_type}: {probability:.2%}")
    else:
        print("\nCould not generate predictions. Check logs/errors above.")