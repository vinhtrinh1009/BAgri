import 'package:json_annotation/json_annotation.dart';

part 'create_farmer_param.g.dart';

@JsonSerializable()
class CreateFarmerParam {
  @JsonKey(name: 'manager_id')
  String? managerId;
  @JsonKey(name: 'workday_id')
  String? workdayId;
  @JsonKey(name: 'fullname')
  String? fullName;

  String? phone;

  factory CreateFarmerParam.fromJson(Map<String, dynamic> json) =>
      _$CreateFarmerParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateFarmerParamToJson(this);

  CreateFarmerParam({
    this.managerId,
    this.workdayId,
    this.fullName,
    this.phone,
  });

  CreateFarmerParam copyWith({
    String? managerId,
    String? workdayId,
    String? fullName,
    String? phone,
  }) {
    return CreateFarmerParam(
      managerId: managerId ?? this.managerId,
      workdayId: workdayId ?? this.workdayId,
      fullName: fullName ?? this.fullName,
      phone: phone ?? this.phone,
    );
  }
}
