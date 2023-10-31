import 'package:json_annotation/json_annotation.dart';

part 'season_entity.g.dart';

@JsonSerializable()
class SeasonEntity {
  String? season_id;
  String? name;

  factory SeasonEntity.fromJson(Map<String, dynamic> json) =>
      _$SeasonEntityFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonEntityToJson(this);

  SeasonEntity({
    this.season_id,
    this.name,
  });

  SeasonEntity copyWith({
    String? season_id,
    String? name,
  }) {
    return SeasonEntity(
      season_id: season_id ?? this.season_id,
      name: name ?? this.name,
    );
  }
}
