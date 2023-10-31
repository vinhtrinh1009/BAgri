import 'package:flutter_base/models/entities/manager/manager_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'farmer_detail_entity.g.dart';

@JsonSerializable()
class FarmerDetailResponse {
  FarmerDetailEntity? farmer;

  factory FarmerDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$FarmerDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerDetailResponseToJson(this);

  FarmerDetailResponse({
    this.farmer,
  });

  FarmerDetailResponse copyWith({
    FarmerDetailEntity? farmer,
  }) {
    return FarmerDetailResponse(
      farmer: farmer ?? this.farmer,
    );
  }
}

@JsonSerializable()
class FarmerDetailEntity {
  String? fullname;
  String? phone;
  String? farmer_id;
  dynamic workdays;
  ManagerEntity? manager;
  List<TaskEntity>? tasks;

  factory FarmerDetailEntity.fromJson(Map<String, dynamic> json) =>
      _$FarmerDetailEntityFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerDetailEntityToJson(this);

  FarmerDetailEntity({
    this.fullname,
    this.phone,
    this.farmer_id,
    this.workdays,
    this.manager,
    this.tasks,
  });

  FarmerDetailEntity copyWith({
    String? fullname,
    String? phone,
    String? farmer_id,
    dynamic workdays,
    ManagerEntity? manager,
    List<TaskEntity>? tasks,
  }) {
    return FarmerDetailEntity(
      fullname: fullname ?? this.fullname,
      phone: phone ?? this.phone,
      farmer_id: farmer_id ?? this.farmer_id,
      workdays: workdays ?? this.workdays,
      manager: manager ?? this.manager,
      tasks: tasks ?? this.tasks,
    );
  }
}

@JsonSerializable()
class TaskEntity {
  String? task_id;
  String? start_time;
  String? end_time;
  String? date;
  String? name;

  @JsonKey(ignore: true)
  DateTime? dateTime;

  factory TaskEntity.fromJson(Map<String, dynamic> json) =>
      _$TaskEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TaskEntityToJson(this);

  TaskEntity({
    this.task_id,
    this.start_time,
    this.end_time,
    this.date,
    this.name,
    this.dateTime,
  });

  TaskEntity copyWith({
    String? task_id,
    String? start_time,
    String? end_time,
    String? date,
    String? name,
    DateTime? dateTime,
  }) {
    return TaskEntity(
      task_id: task_id ?? this.task_id,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      date: date ?? this.date,
      name: name ?? this.name,
      dateTime: dateTime ?? this.dateTime,
    );
  }
}
