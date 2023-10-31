import 'package:json_annotation/json_annotation.dart';

part 'manager_entity.g.dart';

@JsonSerializable()
class ManagerEntity {
  String? manager_id;
  String? fullname;
  String? id;

  factory ManagerEntity.fromJson(Map<String, dynamic> json) =>
      _$ManagerEntityFromJson(json);
  Map<String, dynamic> toJson() => _$ManagerEntityToJson(this);

  ManagerEntity({
    this.manager_id,
    this.fullname,
    this.id,
  });

  ManagerEntity copyWith({
    String? manager_id,
    String? fullname,
    String? id,
  }) {
    return ManagerEntity(
      manager_id: manager_id ?? this.manager_id,
      fullname: fullname ?? this.fullname,
      id: id ?? this.id,
    );
  }
}

@JsonSerializable()
class ManagerListResponse {
  List<ManagerEntity>? managers;

  factory ManagerListResponse.fromJson(Map<String, dynamic> json) =>
      _$ManagerListResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ManagerListResponseToJson(this);

  ManagerListResponse({
    this.managers,
  });

  ManagerListResponse copyWith({
    List<ManagerEntity>? managers,
  }) {
    return ManagerListResponse(
      managers: managers ?? this.managers,
    );
  }
}
