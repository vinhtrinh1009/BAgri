import 'package:flutter_base/models/entities/garden/season_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:json_annotation/json_annotation.dart';

part 'garden_entity.g.dart';

@JsonSerializable()
class GardenListResponse {
  @JsonKey()
  List<GardenEntity>? gardens;

  GardenListResponse({
    this.gardens,
  });

  GardenListResponse copyWith({
    List<GardenEntity>? gardens,
  }) {
    return GardenListResponse(
      gardens: gardens ?? this.gardens,
    );
  }

  factory GardenListResponse.fromJson(Map<String, dynamic> json) =>
      _$GardenListResponseFromJson(json);
  Map<String, dynamic> toJson() => _$GardenListResponseToJson(this);
}

@JsonSerializable()
class GardenEntity {
  String? id;
  @JsonKey()
  String? garden_id;
  @JsonKey()
  String? name;
  @JsonKey()
  int? area;
  ProcessEntity? process;
  SeasonEntity? season;

  factory GardenEntity.fromJson(Map<String, dynamic> json) =>
      _$GardenEntityFromJson(json);
  Map<String, dynamic> toJson() => _$GardenEntityToJson(this);

  GardenEntity({
    this.id,
    this.garden_id,
    this.name,
    this.area,
    this.process,
    this.season,
  });

  GardenEntity copyWith({
    String? id,
    String? garden_id,
    String? name,
    int? area,
    ProcessEntity? process,
    SeasonEntity? season,
  }) {
    return GardenEntity(
      id: id ?? this.id,
      garden_id: garden_id ?? this.garden_id,
      name: name ?? this.name,
      area: area ?? this.area,
      process: process ?? this.process,
      season: season ?? this.season,
    );
  }
}
