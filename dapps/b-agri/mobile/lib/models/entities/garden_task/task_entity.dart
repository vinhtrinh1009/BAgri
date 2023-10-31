import 'package:json_annotation/json_annotation.dart';
part 'task_entity.g.dart';

@JsonSerializable()
class TaskEntity {
  String? task_id;
  String? start_time;
  String? end_time;
  String? date;
  String? name;

  factory TaskEntity.fromJson(Map<String, dynamic> json) =>
      _$TaskEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TaskEntityToJson(this);

  TaskEntity({
    this.task_id,
    this.start_time,
    this.end_time,
    this.date,
    this.name,
  });

  TaskEntity copyWith({
    String? task_id,
    String? start_time,
    String? end_time,
    String? date,
    String? name,
  }) {
    return TaskEntity(
      task_id: task_id ?? this.task_id,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      date: date ?? this.date,
      name: name ?? this.name,
    );
  }
}
