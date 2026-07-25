import 'dart:convert';
import 'package:http/http.dart' as http;

import '../constants/api_config.dart';
import '../models/freelancer_profile.dart';
import '../models/prediction_result.dart';

/// Handles all communication with the backend prediction API.
/// Keeping this separate from the UI means the screen widget doesn't need
/// to know anything about HTTP, JSON, or error-shape parsing.
class PredictionService {
  Future<PredictionResult> predict(FreelancerProfile profile) async {
    try {
      final response = await http
          .post(
            Uri.parse(ApiConfig.predictEndpoint),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(profile.toJson()),
          )
          .timeout(ApiConfig.requestTimeout);

      final Map<String, dynamic> data = jsonDecode(response.body);

      if (response.statusCode == 200) {
        final double rate = (data['predicted_hourly_rate_usd'] as num).toDouble();
        final String model = (data['model_used'] as String?) ?? 'model';
        return PredictionResult.success(predictedRate: rate, modelUsed: model);
      }

      return PredictionResult.failure(_extractErrorMessage(data));
    } catch (e) {
      return PredictionResult.failure(
        'Could not reach the API. Check your connection or the API URL.\n($e)',
      );
    }
  }

  /// Handles FastAPI's two error shapes:
  ///  - {"detail": "some string"}                 (plain HTTPException)
  ///  - {"detail": [{"msg": "...", "loc": [...]}]} (Pydantic validation errors)
  String _extractErrorMessage(Map<String, dynamic> data) {
    final detail = data['detail'];

    if (detail is String) return detail;

    if (detail is List) {
      return detail.map((e) {
        final loc = (e['loc'] as List?)?.join(' -> ') ?? '';
        final msg = e['msg'] ?? 'Invalid value';
        return '$loc: $msg';
      }).join('\n');
    }

    return 'Something went wrong (${data.toString()})';
  }
}
