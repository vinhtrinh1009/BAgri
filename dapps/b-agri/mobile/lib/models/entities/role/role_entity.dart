import 'package:equatable/equatable.dart';
import 'package:json_annotation/json_annotation.dart';
part 'role_entity.g.dart';

@JsonSerializable()
class RoleEntity extends Equatable {
  @JsonKey()
  String? role_id;
  @JsonKey()
  String? name;

  RoleEntity({
    this.role_id,
    this.name,
  });

  RoleEntity copyWith({
    String? role_id,
    String? name,
  }) {
    return RoleEntity(
      role_id: role_id ?? this.role_id,
      name: name ?? this.name,
    );
  }

  factory RoleEntity.fromJson(Map<String, dynamic> json) =>
      _$RoleEntityFromJson(json);
  Map<String, dynamic> toJson() => _$RoleEntityToJson(this);

  @override
  // TODO: implement props
  List<Object?> get props => [role_id, name];
}
