import 'package:json_annotation/json_annotation.dart';

part 'farmer.g.dart';

@JsonSerializable()
class FarmerList {
  String? status;
  FarmerListData? data;

  factory FarmerList.fromJson(Map<String, dynamic> json) =>
      _$FarmerListFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerListToJson(this);

  FarmerList({
    this.status,
    this.data,
  });

  FarmerList copyWith({
    String? status,
    FarmerListData? data,
  }) {
    return FarmerList(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }
}

@JsonSerializable()
class FarmerListData {
  List<FarmerEntity>? farmers;

  factory FarmerListData.fromJson(Map<String, dynamic> json) =>
      _$FarmerListDataFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerListDataToJson(this);

  FarmerListData({
    this.farmers,
  });

  FarmerListData copyWith({
    List<FarmerEntity>? farmers,
  }) {
    return FarmerListData(
      farmers: farmers ?? this.farmers,
    );
  }
}

@JsonSerializable()
class FarmerCreateResponse {
  FarmerEntity? farmer;

  factory FarmerCreateResponse.fromJson(Map<String, dynamic> json) =>
      _$FarmerCreateResponseFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerCreateResponseToJson(this);

  FarmerCreateResponse({
    this.farmer,
  });

  FarmerCreateResponse copyWith({
    FarmerEntity? farmer,
  }) {
    return FarmerCreateResponse(
      farmer: farmer ?? this.farmer,
    );
  }
}

@JsonSerializable()
class FarmerUpdateResponse {
  FarmerEntity? updated_farmer;

  factory FarmerUpdateResponse.fromJson(Map<String, dynamic> json) =>
      _$FarmerUpdateResponseFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerUpdateResponseToJson(this);

  FarmerUpdateResponse({
    this.updated_farmer,
  });

  FarmerUpdateResponse copyWith({
    FarmerEntity? updated_farmer,
  }) {
    return FarmerUpdateResponse(
      updated_farmer: updated_farmer ?? this.updated_farmer,
    );
  }
}

@JsonSerializable()
class FarmerEntity {
  @JsonKey(name: 'farmer_id')
  String? farmerId;
  @JsonKey(name: 'manager_id')
  String? managerId;
  @JsonKey(name: 'workday_id')
  String? workdayId;
  @JsonKey(name: 'fullname')
  String? fullName;
  String? phone;

  FarmerEntity({
    this.farmerId,
    this.managerId,
    this.workdayId,
    this.fullName,
    this.phone,
  });
  factory FarmerEntity.fromJson(Map<String, dynamic> json) =>
      _$FarmerEntityFromJson(json);
  Map<String, dynamic> toJson() => _$FarmerEntityToJson(this);

  FarmerEntity copyWith({
    String? farmerId,
    String? managerId,
    String? workdayId,
    String? fullName,
    String? phone,
  }) {
    return FarmerEntity(
      farmerId: farmerId ?? this.farmerId,
      managerId: managerId ?? this.managerId,
      workdayId: workdayId ?? this.workdayId,
      fullName: fullName ?? this.fullName,
      phone: phone ?? this.phone,
    );
  }
}
