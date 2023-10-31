import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:json_annotation/json_annotation.dart';
part 'create_process_params.g.dart';

@JsonSerializable()
class CreateProcessParam {
  @JsonKey()
  String? name;
  @JsonKey()
  List<String>? tree_ids;
  @JsonKey()
  List<StagesParamsEntity>? stages;

  CreateProcessParam({
    this.name,
    this.tree_ids,
    this.stages,
  });

  CreateProcessParam copyWith({
    String? name,
    List<String>? tree_ids,
    List<StagesParamsEntity>? stages,
  }) {
    return CreateProcessParam(
      name: name ?? this.name,
      tree_ids: tree_ids ?? this.tree_ids,
      stages: stages ?? this.stages,
    );
  }

  factory CreateProcessParam.fromJson(Map<String, dynamic> json) =>
      _$CreateProcessParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateProcessParamToJson(this);
}

@JsonSerializable()
class StagesParamsEntity {
  String? name;
  String? stage_id;
  List<StepEntity>? steps;

  StagesParamsEntity({
    this.name,
    this.steps,
    this.stage_id,
  });

  StagesParamsEntity copyWith({
    String? name,
    String? stage_id,
    List<StepEntity>? steps,
  }) {
    return StagesParamsEntity(
      name: name ?? this.name,
      stage_id: stage_id ?? this.stage_id,
      steps: steps ?? this.steps,
    );
  }

  factory StagesParamsEntity.fromJson(Map<String, dynamic> json) =>
      _$StagesParamsEntityFromJson(json);

  Map<String, dynamic> toJson() => _$StagesParamsEntityToJson(this);
}
