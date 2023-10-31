import 'package:json_annotation/json_annotation.dart';

part 'garden_delete.g.dart';

@JsonSerializable()
class GardenDeleteResponse {
  @JsonKey()
  String? status;
  @JsonKey()
  GardenDeleteDataEntity? data;

  GardenDeleteResponse({
    this.status,
    this.data,
  });

  GardenDeleteResponse copyWith({
    String? status,
    GardenDeleteDataEntity? data,
  }) {
    return GardenDeleteResponse(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory GardenDeleteResponse.fromJson(Map<String, dynamic> json) =>
      _$GardenDeleteResponseFromJson(json);
  Map<String, dynamic> toJson() => _$GardenDeleteResponseToJson(this);
}

@JsonSerializable()
class GardenDeleteDataEntity {
  @JsonKey()
  String? garden_id;

  GardenDeleteDataEntity({
    this.garden_id,
  });

  GardenDeleteDataEntity copyWith({
    String? garden_id,
  }) {
    return GardenDeleteDataEntity(
      garden_id: garden_id ?? this.garden_id,
    );
  }

  factory GardenDeleteDataEntity.fromJson(Map<String, dynamic> json) =>
      _$GardenDeleteDataEntityFromJson(json);
  Map<String, dynamic> toJson() => _$GardenDeleteDataEntityToJson(this);
}
