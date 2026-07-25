// Outcome of calling the prediction API: either a successful prediction
// with a rate and the model that produced it, or a failure with a
// human-readable error message.
class PredictionResult {
  final bool success;
  final double? predictedRate;
  final String? modelUsed;
  final String? errorMessage;

  const PredictionResult.success({
    required double predictedRate,
    required String modelUsed,
  })  : success = true,
        predictedRate = predictedRate,
        modelUsed = modelUsed,
        errorMessage = null;

  const PredictionResult.failure(String errorMessage)
      : success = false,
        predictedRate = null,
        modelUsed = null,
        errorMessage = errorMessage;

  // Ready-to-display text for the success case.
  String get displayText =>
      'Predicted hourly rate: \$${predictedRate!.toStringAsFixed(2)} USD\n(via $modelUsed)';
}
