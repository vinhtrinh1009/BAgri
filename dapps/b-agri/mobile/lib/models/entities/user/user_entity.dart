import 'package:json_annotation/json_annotation.dart';

part 'user_entity.g.dart';

// @JsonSerializable()
// class UserInfoResponse {
//   UserEntity? me;
//
//   UserInfoResponse({
//     this.me,
//   });
//
//   UserInfoResponse copyWith({
//     UserEntity? me,
//   }) {
//     return UserInfoResponse(
//       me: me ?? this.me,
//     );
//   }
//
//   factory UserInfoResponse.fromJson(Map<String, dynamic> json) =>
//       _$UserInfoResponseFromJson(json);
//   Map<String, dynamic> toJson() => _$UserInfoResponseToJson(this);
// }

@JsonSerializable()
class UserEntity {
  String? id;
  String? username;
  String? fullname;
  String? role;

  UserEntity({
    this.id,
    this.username,
    this.fullname,
    this.role,
  });

  UserEntity copyWith({
    String? id,
    String? username,
    String? fullname,
    String? role,
  }) {
    return UserEntity(
      id: id ?? this.id,
      username: username ?? this.username,
      fullname: fullname ?? this.fullname,
      role: role ?? this.role,
    );
  }

  factory UserEntity.fromJson(Map<String, dynamic> json) =>
      _$UserEntityFromJson(json);
  Map<String, dynamic> toJson() => _$UserEntityToJson(this);
}
