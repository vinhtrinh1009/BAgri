import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'task.g.dart';

@JsonSerializable()
class TaskListData {
  List<TaskEntity>? tasks;

  TaskListData({
    this.tasks,
  });

  TaskListData copyWith({
    List<TaskEntity>? tasks,
  }) {
    return TaskListData(
      tasks: tasks ?? this.tasks,
    );
  }

  factory TaskListData.fromJson(Map<String, dynamic> json) =>
      _$TaskListDataFromJson(json);
  Map<String, dynamic> toJson() => _$TaskListDataToJson(this);
}
