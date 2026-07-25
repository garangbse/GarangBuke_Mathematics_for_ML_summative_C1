import 'package:flutter/material.dart';

/// A single labeled input field with a hint and optional numeric-range
/// validation. Used for all 8 prediction inputs so the form-building code
/// in the screen stays short and consistent.
class LabeledTextField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final String hint;
  final TextInputType keyboardType;
  final double? min;
  final double? max;

  const LabeledTextField({
    super.key,
    required this.controller,
    required this.label,
    required this.hint,
    this.keyboardType = TextInputType.text,
    this.min,
    this.max,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: TextFormField(
        controller: controller,
        keyboardType: keyboardType,
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          border: const OutlineInputBorder(),
          isDense: true,
        ),
        validator: _validate,
      ),
    );
  }

  String? _validate(String? value) {
    if (value == null || value.trim().isEmpty) {
      return 'Required';
    }

    final effectiveMin = min;
    final effectiveMax = max;
    if (effectiveMin != null && effectiveMax != null) {
      final parsed = double.tryParse(value.trim());
      if (parsed == null) return 'Enter a number';
      if (parsed < effectiveMin || parsed > effectiveMax) {
        return 'Must be between $effectiveMin and $effectiveMax';
      }
    }

    return null;
  }
}
