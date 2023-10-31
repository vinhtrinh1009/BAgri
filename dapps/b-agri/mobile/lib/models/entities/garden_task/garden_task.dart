import 'package:flutter_base/models/entities/garden_task/task_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'garden_task.g.dart';

@JsonSerializable()
class GardenTaskList {
  List<TaskEntity>? tasks;

  GardenTaskList({
    this.tasks,
  });

  GardenTaskList copyWith({
    List<TaskEntity>? tasks,
  }) {
    return GardenTaskList(
      tasks: tasks ?? this.tasks,
    );
  }

  factory GardenTaskList.fromJson(Map<String, dynamic> json) =>
      _$GardenTaskListFromJson(json);
  Map<String, dynamic> toJson() => _$GardenTaskListToJson(this);
}
