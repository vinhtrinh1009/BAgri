import 'package:json_annotation/json_annotation.dart';
part 'create_garden_params.g.dart';

@JsonSerializable()
class CreateGardenParam {
  @JsonKey()
  String? name;
  @JsonKey()
  String? area;
  @JsonKey()
  String? manager_id;

  CreateGardenParam({this.name, this.area, this.manager_id});

  CreateGardenParam copyWith({
    String? name,
    String? area,
    String? manager_id,
  }) {
    return CreateGardenParam(
      name: name ?? this.name,
      area: area ?? this.area,
      manager_id: manager_id ?? this.manager_id,
    );
  }

  factory CreateGardenParam.fromJson(Map<String, dynamic> json) =>
      _$CreateGardenParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateGardenParamToJson(this);
}
