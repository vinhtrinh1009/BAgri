import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'season_steps_response.g.dart';

@JsonSerializable()
class SeasonStepsResponse {
  List<StepEntity>? steps;

  factory SeasonStepsResponse.fromJson(Map<String, dynamic> json) =>
      _$SeasonStepsResponseFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonStepsResponseToJson(this);

  SeasonStepsResponse({
    this.steps,
  });

  SeasonStepsResponse copyWith({
    List<StepEntity>? steps,
  }) {
    return SeasonStepsResponse(
      steps: steps ?? this.steps,
    );
  }
}
