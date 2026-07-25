import 'package:flutter/material.dart';

/// The display area that shows either the predicted value, an error
/// message, or a neutral placeholder before the first prediction.
class ResultDisplay extends StatelessWidget {
  final String? resultText;
  final bool isError;

  const ResultDisplay({
    super.key,
    required this.resultText,
    required this.isError,
  });

  @override
  Widget build(BuildContext context) {
    final bool hasResult = resultText != null;

    final Color backgroundColor = !hasResult
        ? Colors.grey.shade100
        : (isError ? Colors.red.shade50 : Colors.green.shade50);

    final Color borderColor = !hasResult
        ? Colors.grey.shade300
        : (isError ? Colors.red.shade200 : Colors.green.shade200);

    final Color textColor = !hasResult
        ? Colors.grey.shade600
        : (isError ? Colors.red.shade800 : Colors.green.shade800);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: borderColor),
      ),
      child: Text(
        resultText ?? 'Prediction result will appear here.',
        style: TextStyle(
          fontSize: 15,
          color: textColor,
          fontWeight: hasResult ? FontWeight.w600 : FontWeight.normal,
        ),
      ),
    );
  }
}
