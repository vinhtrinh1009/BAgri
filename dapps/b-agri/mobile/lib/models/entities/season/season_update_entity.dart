import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:json_annotation/json_annotation.dart';

part 'season_update_entity.g.dart';

@JsonSerializable()
class SeasonUpdateResponse {
  SeasonEntity? updated_season;

  factory SeasonUpdateResponse.fromJson(Map<String, dynamic> json) =>
      _$SeasonUpdateResponseFromJson(json);
  Map<String, dynamic> toJson() => _$SeasonUpdateResponseToJson(this);

  SeasonUpdateResponse({
    this.updated_season,
  });

  SeasonUpdateResponse copyWith({
    SeasonEntity? updated_season,
  }) {
    return SeasonUpdateResponse(
      updated_season: updated_season ?? this.updated_season,
    );
  }
}
