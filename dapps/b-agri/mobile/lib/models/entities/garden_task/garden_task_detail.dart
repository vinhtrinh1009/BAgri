import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/process/step_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'garden_task_detail.g.dart';

@JsonSerializable()
class GardenTaskDetailResponse {
  TaskDetailEntity? task;

  GardenTaskDetailResponse({
    this.task,
  });

  GardenTaskDetailResponse copyWith({
    TaskDetailEntity? task,
  }) {
    return GardenTaskDetailResponse(
      task: task ?? this.task,
    );
  }

  factory GardenTaskDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$GardenTaskDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$GardenTaskDetailResponseToJson(this);
}

@JsonSerializable()
class TaskDetailEntity {
  StepEntity? step;
  String? name;
  String? task_id;
  String? manager_id;
  String? season_id;
  String? date;
  String? description;
  String? start_time;
  String? end_time;
  List<String>? result;
  // List<String>? items;
  String? items;
  List<FarmerEntity>? farmers;

  factory TaskDetailEntity.fromJson(Map<String, dynamic> json) =>
      _$TaskDetailEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TaskDetailEntityToJson(this);

  TaskDetailEntity({
    this.step,
    this.name,
    this.task_id,
    this.manager_id,
    this.season_id,
    this.date,
    this.description,
    this.start_time,
    this.end_time,
    this.result,
    this.items,
    this.farmers,
  });

  TaskDetailEntity copyWith({
    StepEntity? step,
    String? name,
    String? task_id,
    String? manager_id,
    String? season_id,
    String? date,
    String? description,
    String? start_time,
    String? end_time,
    List<String>? result,
    // List<String>? items,
    String? items,
    List<FarmerEntity>? farmers,
  }) {
    return TaskDetailEntity(
      step: step ?? this.step,
      name: name ?? this.name,
      task_id: task_id ?? this.task_id,
      manager_id: manager_id ?? this.manager_id,
      season_id: season_id ?? this.season_id,
      date: date ?? this.date,
      description: description ?? this.description,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      result: result ?? this.result,
      items: items ?? this.items,
      farmers: farmers ?? this.farmers,
    );
  }
}
