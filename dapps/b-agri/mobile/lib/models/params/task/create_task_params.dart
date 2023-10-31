import 'package:json_annotation/json_annotation.dart';
part 'create_task_params.g.dart';

@JsonSerializable()
class CreateTaskParam {
  String? manager_id;
  String? season_id;
  List<String>? farmer_ids;
  String? name;
  String? step_id;
  String? description;
  String? date;
  String? start_time;
  String? end_time;
  List<String>? result;
  String? items;

  CreateTaskParam({
    this.manager_id,
    this.season_id,
    this.farmer_ids,
    this.name,
    this.step_id,
    this.description,
    this.date,
    this.start_time,
    this.end_time,
    this.result,
    this.items,
  });

  CreateTaskParam copyWith({
    String? manager_id,
    String? season_id,
    List<String>? farmer_ids,
    String? name,
    String? step_id,
    String? description,
    String? date,
    String? start_time,
    String? end_time,
    List<String>? result,
    String? items,
  }) {
    return CreateTaskParam(
      manager_id: manager_id ?? this.manager_id,
      season_id: season_id ?? this.season_id,
      farmer_ids: farmer_ids ?? this.farmer_ids,
      name: name ?? this.name,
      step_id: step_id ?? this.step_id,
      description: description ?? this.description,
      date: date ?? this.date,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      result: result ?? this.result,
      items: items ?? this.items,
    );
  }

  factory CreateTaskParam.fromJson(Map<String, dynamic> json) =>
      _$CreateTaskParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateTaskParamToJson(this);
}
