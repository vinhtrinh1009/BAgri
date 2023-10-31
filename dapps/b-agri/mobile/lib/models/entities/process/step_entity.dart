import 'package:equatable/equatable.dart';
import 'package:json_annotation/json_annotation.dart';

part 'step_entity.g.dart';

@JsonSerializable()
class StepEntity extends Equatable {
  String? step_id;
  int? from_day;
  int? to_day;
  String? name;
  String? stage_id;
  int? actual_day;

  @JsonKey(ignore: true)
  int? startDay;
  @JsonKey(ignore: true)
  int? endDay;

  factory StepEntity.fromJson(Map<String, dynamic> json) =>
      _$StepEntityFromJson(json);
  Map<String, dynamic> toJson() => _$StepEntityToJson(this);

  @override
  List<Object?> get props =>
      [step_id, from_day, to_day, name, stage_id, actual_day];

  StepEntity({
    this.step_id,
    this.from_day,
    this.to_day,
    this.name,
    this.stage_id,
    this.actual_day,
    this.startDay,
    this.endDay,
  });

  StepEntity copyWith({
    String? step_id,
    int? from_day,
    int? to_day,
    String? name,
    String? stage_id,
    int? actual_day,
    int? startDay,
    int? endDay,
  }) {
    return StepEntity(
      step_id: step_id ?? this.step_id,
      from_day: from_day ?? this.from_day,
      to_day: to_day ?? this.to_day,
      name: name ?? this.name,
      stage_id: stage_id ?? this.stage_id,
      actual_day: actual_day ?? this.actual_day,
      startDay: startDay ?? this.startDay,
      endDay: endDay ?? this.endDay,
    );
  }
}
