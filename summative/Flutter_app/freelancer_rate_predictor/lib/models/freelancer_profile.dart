// Represents the 8 input variables the prediction model needs,
// collected from the form fields on the prediction screen.
class FreelancerProfile {
  final String gender;
  final int age;
  final String country;
  final String primarySkill;
  final double yearsOfExperience;
  final double rating;
  final bool isActive;
  final double clientSatisfaction;

  const FreelancerProfile({
    required this.gender,
    required this.age,
    required this.country,
    required this.primarySkill,
    required this.yearsOfExperience,
    required this.rating,
    required this.isActive,
    required this.clientSatisfaction,
  });

  // Matches the field names expected by the API's Pydantic
  // PredictionRequest schema exactly.
  Map<String, dynamic> toJson() {
    return {
      'gender': gender,
      'age': age,
      'country': country,
      'primary_skill': primarySkill,
      'years_of_experience': yearsOfExperience,
      'rating': rating,
      'is_active': isActive,
      'client_satisfaction': clientSatisfaction,
    };
  }
}
