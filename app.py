from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Phase-specific features
phase_features = {
    "phase_1": ['FF', 'APUF_Mean', 'GS_Mean', 'Distance'],
    "phase_2": ['FF', 'N1T_Mean', 'GS_Mean', 'SAT', 'Distance'],
    "phase_3": ['FF', 'N1T_Mean', 'TAT', 'PS_Mean', 'Distance'],
    "phase_4": ['FF', 'N1T_Mean', 'ALTR_Mean', 'GS_Mean', 'Distance'],
    "phase_5": ['FF', 'TAS_Mean', 'MACH_Mean', 'TAT', 'Distance'],
    "phase_6": ['FF', 'GS_Mean', 'TAT', 'PT_Mean', 'Distance'],
    "phase_7": ['FF', 'GS_Mean', 'TRKM_Mean', 'LATP', 'Distance']
}

# Phase names mapping
phase_names = {
    "phase_1": "takeoff",
    "phase_2": "initial_climb",
    "phase_3": "climb",
    "phase_4": "cruise",
    "phase_5": "descent",
    "phase_6": "approach",
    "phase_7": "landing"
}

# Load models and scalers
models = {}
scalers = {}

print("\n=== Loading Models and Scalers ===")
for phase in phase_features.keys():
    model_path = os.path.join('phasewise_models', f'model_{phase}.joblib')
    scaler_path = os.path.join('phasewise_scaler', f'scaler_{phase}.joblib')
    
    print(f"\nChecking {phase}:")
    print(f"Model path: {model_path}")
    print(f"Scaler path: {scaler_path}")
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        try:
            models[phase] = joblib.load(model_path)
            scalers[phase] = joblib.load(scaler_path)
            print(f"Successfully loaded model and scaler for {phase}")
        except Exception as e:
            print(f"Error loading model or scaler for {phase}: {str(e)}")
    else:
        print(f"Warning: Model or scaler not found for {phase}")
        if not os.path.exists(model_path):
            print(f"Missing model file: {model_path}")
        if not os.path.exists(scaler_path):
            print(f"Missing scaler file: {scaler_path}")

print("\nLoaded models for phases:", list(models.keys()))
print("Loaded scalers for phases:", list(scalers.keys()))

@app.route('/')
def home():
    return render_template('index.html', phase_features=phase_features)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def validate_input(data, required_features):
    """Validate input data against required features"""
    missing_features = [feat for feat in required_features if feat not in data]
    if missing_features:
        return False, f"Missing features: {', '.join(missing_features)}"
    return True, None

def prepare_input(data, features, scaler):
    """Prepare input data for model prediction"""
    input_data = [[float(data[feature]) for feature in features]]
    return scaler.transform(input_data)

@app.route('/get_phase_features', methods=['GET'])
def get_phase_features():
    """Return the features required for each phase"""
    return jsonify(phase_features)

@app.route('/predict_single_phase', methods=['POST'])
def predict_single_phase():
    try:
        print("=== Starting predict_single_phase ===")
        data = request.json
        phase = data.get('phase')
        input_data = data.get('input_data')

        print(f"Received phase: {phase}")
        print(f"Received input data: {input_data}")
        print(f"Available models: {list(models.keys())}")
        print(f"Phase names mapping: {phase_names}")

        # Map phase name to phase number
        phase_num = next((k for k, v in phase_names.items() if v == phase), None)
        print(f"Mapped phase number: {phase_num}")

        if not phase_num:
            print(f"Phase mapping not found for {phase}")
            return jsonify({'error': f'Invalid phase name: {phase}'}), 400
        
        if phase_num not in models:
            print(f"Model not found for phase {phase_num}")
            return jsonify({'error': f'Model not found for {phase}'}), 400

        # Validate input
        required_features = phase_features[phase_num]
        print(f"Required features: {required_features}")
        
        is_valid, error_message = validate_input(input_data, required_features)
        if not is_valid:
            print(f"Input validation failed: {error_message}")
            return jsonify({'error': error_message}), 400

        # Prepare input and make prediction
        X = prepare_input(input_data, required_features, scalers[phase_num])
        prediction = models[phase_num].predict(X)[0]

        print(f"Prediction successful: {prediction}")
        return jsonify({
            'phase': phase,
            'predicted_fuel': float(prediction),
            'units': 'gallons'
        })

    except Exception as e:
        print(f"Error in predict_single_phase: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_all_phases', methods=['POST'])
def predict_all_phases():
    try:
        data = request.json
        input_data = data.get('input_data')
        predictions = {}
        total_fuel = 0

        for phase_num, features in phase_features.items():
            # Validate input for this phase
            is_valid, error_message = validate_input(input_data, features)
            if not is_valid:
                return jsonify({'error': f'For {phase_names[phase_num]}: {error_message}'}), 400

            # Prepare input and make prediction
            X = prepare_input(input_data, features, scalers[phase_num])
            pred = models[phase_num].predict(X)[0]
            
            predictions[phase_names[phase_num]] = float(pred)
            total_fuel += pred

        return jsonify({
            'phase_predictions': predictions,
            'total_fuel': float(total_fuel),
            'units': 'gallons'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
