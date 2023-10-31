import 'package:json_annotation/json_annotation.dart';

part 'login_model.g.dart';

@JsonSerializable()
class LoginResponseEntity {
  @JsonKey()
  String? status;
  @JsonKey()
  TokenEntity? data;

  LoginResponseEntity({
    this.status,
    this.data,
  });

  LoginResponseEntity copyWith({
    String? status,
    TokenEntity? data,
  }) {
    return LoginResponseEntity(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory LoginResponseEntity.fromJson(Map<String, dynamic> json) =>
      _$LoginResponseEntityFromJson(json);
  Map<String, dynamic> toJson() => _$LoginResponseEntityToJson(this);
}

@JsonSerializable()
class TokenEntity {
  @JsonKey()
  String? token;
  @JsonKey()
  String? user_id;

  TokenEntity({
    this.token,
    this.user_id,
  });

  TokenEntity copyWith({
    String? token,
    String? user_id,
  }) {
    return TokenEntity(
      token: token ?? this.token,
      user_id: user_id ?? this.user_id,
    );
  }
  factory TokenEntity.fromJson(Map<String, dynamic> json) =>
      _$TokenEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TokenEntityToJson(this);
}
