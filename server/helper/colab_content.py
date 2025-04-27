import pandas as pd
import numpy as np
import joblib
import os
import glob
from datetime import datetime
import gc
import time

# Removed unused import: from . import utils


def clean_label(label):
    if isinstance(label, str):
        label = label.replace('has_', '')
        label = label.replace('_next_24h_here', '')
        label = label.replace('_', ' ')
    return label


def predict_next_event_probabilities(event_data, models_directory='trained_models', datetime_col='תאריך ושעה פתיחה'):
    print("--- Starting Prediction Function ---")
    if gc.isenabled(): print("Garbage collector is enabled.")
    else: gc.enable(); print("Garbage collector enabled.")

    print(f"Searching for models in: {os.path.abspath(models_directory)}")
    model_files = glob.glob(os.path.join(models_directory, 'pipeline_*.joblib'))
    if not model_files:
        print(f"Error: No model pipeline files ('pipeline_*.joblib') found in '{models_directory}'.")
        print("--- Prediction Function Ended (No Models Found) ---")
        # Raising an error might be better than returning {} if models are expected
        # raise FileNotFoundError(f"No model pipeline files found in '{models_directory}'")
        return {} # Keep original behavior
    print(f"Found {len(model_files)} model pipelines.")
    predictions = {}

    print("Preparing input data...")
    try:
        # Ensure input is treated as a single row
        if isinstance(event_data, dict):
            input_df = pd.DataFrame([event_data])
        elif isinstance(event_data, pd.DataFrame):
            input_df = event_data.head(1).copy() # Ensure it's just one event
        else:
            raise TypeError("event_data must be a dictionary or pandas DataFrame")

        if datetime_col not in input_df.columns:
            # More specific error message
            raise KeyError(f"Input 'event_data' must contain the datetime column specified by datetime_col: '{datetime_col}'")

        # Use infer_datetime_format for potential speedup, handle errors robustly
        input_df[datetime_col] = pd.to_datetime(input_df[datetime_col], errors='coerce', infer_datetime_format=True)
        if input_df[datetime_col].isnull().any():
             # Provide the problematic value if possible (assuming single row)
             bad_value = input_df.loc[input_df[datetime_col].isnull(), datetime_col].iloc[0]
             raise ValueError(f"Invalid or unparseable datetime value '{bad_value}' found in column '{datetime_col}'.")

        dt_series = input_df[datetime_col].dt
        input_df['event_hour'] = dt_series.hour
        input_df['event_dayofweek'] = dt_series.dayofweek
        input_df['event_month'] = dt_series.month

        input_df['hour_sin'] = np.sin(2 * np.pi * input_df['event_hour'] / 24.0)
        input_df['hour_cos'] = np.cos(2 * np.pi * input_df['event_hour'] / 24.0)

        input_df['dayofweek_sin'] = np.sin(2 * np.pi * input_df['event_dayofweek'] / 7.0)
        input_df['dayofweek_cos'] = np.cos(2 * np.pi * input_df['event_dayofweek'] / 7.0)

        input_df['is_weekend'] = input_df['event_dayofweek'].isin([4, 5]).astype(int)

        print("Engineered features created (cyclical time, weekend).")
        print(f"Input DataFrame shape after engineering: {input_df.shape}")
        # print(f"Columns available for pipeline: {input_df.columns.tolist()}")

    # Catch specific expected errors first
    except KeyError as e:
        print(f"Error preparing input data: Missing expected key {e}.")
        print(f"Required raw features should include: latitude, longitude, 'Maximum Temperature (°C)', Gale, 'נושא', 'חג_עברי', and '{datetime_col}'. Check payload keys.")
        print("--- Prediction Function Ended (Input Error) ---")
        # Propagate error for Flask to catch
        raise KeyError(f"Missing expected data key: {e}") from e
        # return {} # Keep original behavior if preferred over raising error
    except (ValueError, TypeError) as e:
         print(f"Error preparing input data: {e}")
         print("--- Prediction Function Ended (Input Error) ---")
         raise ValueError(f"Data format error during preparation: {e}") from e
         # return {}
    except Exception as e:
        print(f"An unexpected error occurred preparing input data: {type(e).__name__}: {e}")
        print("--- Prediction Function Ended (Input Error) ---")
        raise Exception(f"Unexpected error during data preparation: {e}") from e
        # return {}


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

            print(f"  Loading model...", flush=True); start_load_time = time.time()
            model_pipeline = joblib.load(model_path)
            load_time = time.time() - start_load_time; print(f"  Model loaded. ({load_time:.2f}s)", flush=True)

            print(f"  Predicting probability...", flush=True); start_pred_time = time.time()

            # Ensure predict_proba is available and get probability of the positive class (usually index 1)
            if not hasattr(model_pipeline, "predict_proba"):
                 print(f"  ERROR: Model for '{target_col_raw}' does not have a predict_proba method.", flush=True)
                 continue # Skip this model

            probabilities = model_pipeline.predict_proba(input_df)
            # Check shape, assume binary classification [prob_class_0, prob_class_1]
            if probabilities.shape[1] >= 2:
                probability_positive_class = probabilities[0, 1]
            else:
                 # Handle cases where predict_proba might return only one class probability
                 print(f"  Warning: predict_proba for '{target_col_raw}' returned unexpected shape {probabilities.shape}. Using first value.", flush=True)
                 probability_positive_class = probabilities[0, 0]

            pred_time = time.time() - start_pred_time; print(f"  Prediction complete. Prob={probability_positive_class:.4f} ({pred_time:.2f}s)", flush=True)

            cleaned_event_name = clean_label(target_col_raw)
            predictions[cleaned_event_name] = float(probability_positive_class) # Ensure float type


        # Specific Error Handling
        except FileNotFoundError: print(f"  ERROR: Model file not found at expected path {model_path}.", flush=True); continue # Continue loop
        except (joblib.externals.loky.process_executor.TerminatedWorkerError, EOFError, TypeError, ValueError) as e: # Broader catch for loading issues
             print(f"  ERROR: Failed to load/deserialize model '{target_col_raw}' from {model_path}. Check file integrity/compatibility. Error: {type(e).__name__}: {e}", flush=True); continue
        except AttributeError as e: print(f"  ERROR: Problem accessing attribute during prediction for '{target_col_raw}'. Might be model structure issue. Error: {e}", flush=True); continue
        except KeyError as e: print(f"  ERROR predicting for '{target_col_raw}': Required feature {e} not found by pipeline's preprocessor. Check feature engineering alignment.", flush=True); continue # Feature mismatch
        except ValueError as e: print(f"  ERROR during prediction for '{target_col_raw}': {e}. Check data types/values expected by model.", flush=True); continue
        except Exception as e: # Catch unexpected issues during loop
            target_name = target_col_raw or os.path.basename(model_path); print(f"  UNEXPECTED ERROR processing model '{target_name}': {type(e).__name__}: {e}", flush=True); continue # Log and continue
        finally:
            if model_pipeline is not None: del model_pipeline
            collected_count = gc.collect()
            # print(f"  GC collected {collected_count} objects.", flush=True) # Optional: reduce verbosity


    print("\n--- Model Loop Finished ---")
    print(f"Successfully processed {len(predictions)} models out of {len(model_files)} found.")
    if not predictions:
        print("Warning: No predictions were generated. Check logs for errors in each model loop iteration.");
        print("--- Prediction Function Ended (No Results) ---");
        return {} # Return empty if no model succeeded

    print("Sorting results...")
    sorted_predictions = dict(sorted(predictions.items(), key=lambda item: item[1], reverse=True))
    print("Prediction process complete."); print("--- Prediction Function Ended Successfully ---")
    return sorted_predictions


# This function is called by the Flask app
def predict(sample_event, models_directory_path):
    # MODELS_SAVE_DIRECTORY = models_directory_path # Renamed for clarity

    print("Calling predict_next_event_probabilities...")
    # print(sample_event) # Print payload in Flask route instead if sensitive

    # Error handling added around the call
    try:
        event_probabilities = predict_next_event_probabilities(
            event_data=sample_event,
            models_directory=models_directory_path, # Pass the path directly
            datetime_col='תאריך ושעה פתיחה' # Ensure this matches the key in sample_event
        )
    except (FileNotFoundError, KeyError, ValueError, Exception) as e:
        # Log the error from predict_next_event_probabilities if it was raised
        print(f"Error received from predict_next_event_probabilities: {type(e).__name__}: {e}")
        # Depending on desired behavior, re-raise or return empty/error indicator
        # return {"error": str(e)} # Example error indicator
        raise e # Re-raise to be caught by Flask route's error handler

    print("Function call returned.")

    if event_probabilities:
        print("\nPredicted Probabilities for Next Event Types (Sorted):")
        # Limit printing if too many results
        # count = 0
        # for event_type, probability in event_probabilities.items():
        #     print(f"- {event_type}: {probability:.2%}")
        #     count += 1
        #     if count >= 10: print("... (results truncated)"); break
    else:
        print("\nCould not generate predictions. Check logs/errors above.")

    return event_probabilities