import 'package:flutter/material.dart';

import '../models/freelancer_profile.dart';
import '../services/prediction_service.dart';
import '../widgets/labeled_text_field.dart';
import '../widgets/result_display.dart';

// The app's single page: 8 input fields, a Predict button, and a
// display area for the result or an error message.
class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  State<PredictionScreen> createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final _formKey = GlobalKey<FormState>();
  final _predictionService = PredictionService();

  // One controller per input field -- 8 fields = 8 TextFields,
  // matching the 8 variables the prediction model needs.
  final _genderController = TextEditingController();
  final _ageController = TextEditingController();
  final _countryController = TextEditingController();
  final _skillController = TextEditingController();
  final _experienceController = TextEditingController();
  final _ratingController = TextEditingController();
  final _isActiveController = TextEditingController();
  final _satisfactionController = TextEditingController();

  bool _isLoading = false;
  String? _resultText;
  bool _isError = false;

  @override
  void dispose() {
    _genderController.dispose();
    _ageController.dispose();
    _countryController.dispose();
    _skillController.dispose();
    _experienceController.dispose();
    _ratingController.dispose();
    _isActiveController.dispose();
    _satisfactionController.dispose();
    super.dispose();
  }

  bool _parseBool(String value) {
    final v = value.toLowerCase();
    return v == 'true' || v == 'yes' || v == '1';
  }

  Future<void> _handlePredict() async {
    if (!_formKey.currentState!.validate()) {
      setState(() {
        _isError = true;
        _resultText = 'Please fill in all fields with valid values.';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _resultText = null;
      _isError = false;
    });

    final profile = FreelancerProfile(
      gender: _genderController.text.trim(),
      age: int.parse(_ageController.text.trim()),
      country: _countryController.text.trim(),
      primarySkill: _skillController.text.trim(),
      yearsOfExperience: double.parse(_experienceController.text.trim()),
      rating: double.parse(_ratingController.text.trim()),
      isActive: _parseBool(_isActiveController.text.trim()),
      clientSatisfaction: double.parse(_satisfactionController.text.trim()),
    );

    final result = await _predictionService.predict(profile);

    if (!mounted) return;

    setState(() {
      _isLoading = false;
      _isError = !result.success;
      _resultText = result.success ? result.displayText : result.errorMessage;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Freelancer Hourly Rate Predictor'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Enter freelancer details',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),

                LabeledTextField(
                  controller: _genderController,
                  label: 'Gender',
                  hint: 'male or female',
                ),
                LabeledTextField(
                  controller: _ageController,
                  label: 'Age',
                  hint: '18 - 75',
                  keyboardType: TextInputType.number,
                  min: 18,
                  max: 75,
                ),
                LabeledTextField(
                  controller: _countryController,
                  label: 'Country',
                  hint: 'e.g. India, Germany, Brazil',
                ),
                LabeledTextField(
                  controller: _skillController,
                  label: 'Primary Skill',
                  hint: 'e.g. Machine Learning, Web Development',
                ),
                LabeledTextField(
                  controller: _experienceController,
                  label: 'Years of Experience',
                  hint: '0 - 50',
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  min: 0,
                  max: 50,
                ),
                LabeledTextField(
                  controller: _ratingController,
                  label: 'Rating',
                  hint: '0.0 - 5.0',
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  min: 0,
                  max: 5,
                ),
                LabeledTextField(
                  controller: _isActiveController,
                  label: 'Is Active',
                  hint: 'true or false',
                ),
                LabeledTextField(
                  controller: _satisfactionController,
                  label: 'Client Satisfaction (%)',
                  hint: '0 - 100',
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  min: 0,
                  max: 100,
                ),

                const SizedBox(height: 12),
                SizedBox(
                  height: 48,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _handlePredict,
                    child: _isLoading
                        ? const SizedBox(
                            height: 22,
                            width: 22,
                            child: CircularProgressIndicator(
                              strokeWidth: 2.5,
                              color: Colors.white,
                            ),
                          )
                        : const Text('Predict', style: TextStyle(fontSize: 16)),
                  ),
                ),

                const SizedBox(height: 20),
                ResultDisplay(resultText: _resultText, isError: _isError),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
