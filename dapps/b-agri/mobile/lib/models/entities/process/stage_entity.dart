import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'stage_entity.g.dart';

@JsonSerializable()
class StageEntity extends Equatable {
  String? name;
  String? stage_id;
  List<StepEntity>? steps;

  factory StageEntity.fromJson(Map<String, dynamic> json) =>
      _$StageEntityFromJson(json);
  Map<String, dynamic> toJson() => _$StageEntityToJson(this);

  StageEntity({
    this.name,
    this.stage_id,
    this.steps,
  });

  StageEntity copyWith({
    String? name,
    String? stage_id,
    List<StepEntity>? steps,
  }) {
    return StageEntity(
      name: name ?? this.name,
      stage_id: stage_id ?? this.stage_id,
      steps: steps ?? this.steps,
    );
  }

  @override
  List<Object?> get props => [name, steps, stage_id];
}
