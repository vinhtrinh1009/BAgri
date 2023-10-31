import 'package:json_annotation/json_annotation.dart';

part 'season_task_entity.g.dart';

@JsonSerializable()
class SeasonTaskResponse {
  List<SeasonTaskEntity>? tasks;

  SeasonTaskResponse({
    this.tasks,
  });

  factory SeasonTaskResponse.fromJson(Map<String, dynamic> json) =>
      _$SeasonTaskResponseFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonTaskResponseToJson(this);

  SeasonTaskResponse copyWith({
    List<SeasonTaskEntity>? tasks,
  }) {
    return SeasonTaskResponse(
      tasks: tasks ?? this.tasks,
    );
  }
}

@JsonSerializable()
class SeasonTaskEntity {
  String? name;
  String? date;
  String? start_time;
  String? end_time;
  String? task_id;

  SeasonTaskEntity({
    this.name,
    this.date,
    this.start_time,
    this.end_time,
    this.task_id,
  });

  factory SeasonTaskEntity.fromJson(Map<String, dynamic> json) =>
      _$SeasonTaskEntityFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonTaskEntityToJson(this);

  SeasonTaskEntity copyWith({
    String? name,
    String? date,
    String? start_time,
    String? end_time,
    String? task_id,
  }) {
    return SeasonTaskEntity(
      name: name ?? this.name,
      date: date ?? this.date,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      task_id: task_id ?? this.task_id,
    );
  }
}
