import 'package:json_annotation/json_annotation.dart';

part 'garden_detail.g.dart';

@JsonSerializable()
class GardenDetailResponse {
  @JsonKey()
  String? status;
  @JsonKey()
  GardenDetailEntity? data;

  GardenDetailResponse({
    this.status,
    this.data,
  });

  GardenDetailResponse copyWith({
    String? status,
    GardenDetailEntity? data,
  }) {
    return GardenDetailResponse(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory GardenDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$GardenDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$GardenDetailResponseToJson(this);
}

@JsonSerializable()
class GardenDetailEntity {
  @JsonKey()
  GardenItemEntity? garden;

  GardenDetailEntity({
    this.garden,
  });

  GardenDetailEntity copyWith({
    GardenItemEntity? garden,
  }) {
    return GardenDetailEntity(
      garden: garden ?? this.garden,
    );
  }

  factory GardenDetailEntity.fromJson(Map<String, dynamic> json) =>
      _$GardenDetailEntityFromJson(json);
  Map<String, dynamic> toJson() => _$GardenDetailEntityToJson(this);
}

@JsonSerializable()
class GardenItemEntity {
  @JsonKey()
  String? garden_id;
  @JsonKey()
  String? name;
  @JsonKey()
  int? area;
  @JsonKey()
  ManagerEntity? manager;
  @JsonKey()
  List<SeasonWithGardenEntity>? seasons;

  GardenItemEntity({
    this.garden_id,
    this.name,
    this.area,
    this.manager,
    this.seasons,
  });

  GardenItemEntity copyWith({
    String? garden_id,
    String? name,
    int? area,
    ManagerEntity? manager,
    List<SeasonWithGardenEntity>? seasons,
  }) {
    return GardenItemEntity(
      garden_id: garden_id ?? this.garden_id,
      name: name ?? this.name,
      area: area ?? this.area,
      seasons: seasons ?? this.seasons,
    );
  }

  factory GardenItemEntity.fromJson(Map<String, dynamic> json) =>
      _$GardenItemEntityFromJson(json);
  Map<String, dynamic> toJson() => _$GardenItemEntityToJson(this);
}

@JsonSerializable()
class SeasonWithGardenEntity {
  String? name;
  String? season_id;
  String? start_date;
  String? end_date;
  String? status;

  factory SeasonWithGardenEntity.fromJson(Map<String, dynamic> json) =>
      _$SeasonWithGardenEntityFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonWithGardenEntityToJson(this);

  SeasonWithGardenEntity({
    this.name,
    this.season_id,
    this.start_date,
    this.end_date,
    this.status,
  });

  SeasonWithGardenEntity copyWith({
    String? name,
    String? season_id,
    String? start_date,
    String? end_date,
    String? status,
  }) {
    return SeasonWithGardenEntity(
      name: name ?? this.name,
      season_id: season_id ?? this.season_id,
      start_date: start_date ?? this.start_date,
      end_date: end_date ?? this.end_date,
      status: status ?? this.status,
    );
  }
}

@JsonSerializable()
class ManagerEntity {
  String? manager_id;
  String? name;

  factory ManagerEntity.fromJson(Map<String, dynamic> json) =>
      _$ManagerEntityFromJson(json);
  Map<String, dynamic> toJson() => _$ManagerEntityToJson(this);

  ManagerEntity({
    this.manager_id,
    this.name,
  });

  ManagerEntity copyWith({
    String? manager_id,
    String? name,
  }) {
    return ManagerEntity(
      manager_id: manager_id ?? this.manager_id,
      name: name ?? this.name,
    );
  }
}
