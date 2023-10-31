import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'season_task_detail_entity.g.dart';

@JsonSerializable()
class SeasonTaskDetailResponse {
  SeasonTaskDetailEntity? task;

  factory SeasonTaskDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$SeasonTaskDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonTaskDetailResponseToJson(this);

  SeasonTaskDetailResponse({
    this.task,
  });

  SeasonTaskDetailResponse copyWith({
    SeasonTaskDetailEntity? task,
  }) {
    return SeasonTaskDetailResponse(
      task: task ?? this.task,
    );
  }
}

@JsonSerializable()
class SeasonTaskDetailEntity {
  String? manager_id;
  String? season_id;
  String? name;
  StepEntity? step;
  String? description;
  String? date;
  String? start_time;
  String? end_time;
  String? task_id;
  List<FarmerEntity>? farmers;
  String? items;
  List<String>? result;

  factory SeasonTaskDetailEntity.fromJson(Map<String, dynamic> json) =>
      _$SeasonTaskDetailEntityFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonTaskDetailEntityToJson(this);

  SeasonTaskDetailEntity({
    this.manager_id,
    this.season_id,
    this.name,
    this.step,
    this.description,
    this.date,
    this.start_time,
    this.end_time,
    this.task_id,
    this.farmers,
    this.items,
    this.result,
  });

  SeasonTaskDetailEntity copyWith({
    String? manager_id,
    String? season_id,
    String? name,
    StepEntity? step,
    String? description,
    String? date,
    String? start_time,
    String? end_time,
    String? task_id,
    List<FarmerEntity>? farmers,
    String? items,
    List<String>? result,
  }) {
    return SeasonTaskDetailEntity(
      manager_id: manager_id ?? this.manager_id,
      season_id: season_id ?? this.season_id,
      name: name ?? this.name,
      step: step ?? this.step,
      description: description ?? this.description,
      date: date ?? this.date,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      task_id: task_id ?? this.task_id,
      farmers: farmers ?? this.farmers,
      items: items ?? this.items,
      result: result ?? this.result,
    );
  }
}
