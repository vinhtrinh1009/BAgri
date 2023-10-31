import 'package:json_annotation/json_annotation.dart';

part 'task_delete_entity.g.dart';

@JsonSerializable()
class TaskDeleteEntity {
  @JsonKey()
  String? deleted_id;

  TaskDeleteEntity({
    this.deleted_id,
  });

  TaskDeleteEntity copyWith({
    String? deleted_id,
  }) {
    return TaskDeleteEntity(
      deleted_id: deleted_id ?? this.deleted_id,
    );
  }

  factory TaskDeleteEntity.fromJson(Map<String, dynamic> json) =>
      _$TaskDeleteEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TaskDeleteEntityToJson(this);
}
