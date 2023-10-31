import 'package:json_annotation/json_annotation.dart';

part 'create_season_param.g.dart';

@JsonSerializable()
class CreateSeasonParam {
  String? name;
  String? garden_id;
  String? tree_id;
  String? process_id;
  String? start_date;
  String? end_date;
  String? status;

  factory CreateSeasonParam.fromJson(Map<String, dynamic> json) =>
      _$CreateSeasonParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateSeasonParamToJson(this);

  CreateSeasonParam({
    this.name,
    this.garden_id,
    this.tree_id,
    this.process_id,
    this.start_date,
    this.end_date,
    this.status,
  });

  CreateSeasonParam copyWith({
    String? name,
    String? garden_id,
    String? tree_id,
    String? process_id,
    String? start_date,
    String? end_date,
    String? status,
  }) {
    return CreateSeasonParam(
      name: name ?? this.name,
      garden_id: garden_id ?? this.garden_id,
      tree_id: tree_id ?? this.tree_id,
      process_id: process_id ?? this.process_id,
      start_date: start_date ?? this.start_date,
      end_date: end_date ?? this.end_date,
      status: status ?? this.status,
    );
  }
}
