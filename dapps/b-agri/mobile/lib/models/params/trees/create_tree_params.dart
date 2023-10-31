import 'package:json_annotation/json_annotation.dart';
part 'create_tree_params.g.dart';

@JsonSerializable()
class CreateTreeParam {
  @JsonKey()
  String? name;
  @JsonKey()
  String? description;

  CreateTreeParam({
    this.name,
    this.description,
  });

  CreateTreeParam copyWith({
    String? name,
    String? description,
  }) {
    return CreateTreeParam(
      name: name ?? this.name,
      description: description ?? this.description,
    );
  }

  factory CreateTreeParam.fromJson(Map<String, dynamic> json) =>
      _$CreateTreeParamFromJson(json);

  Map<String, dynamic> toJson() => _$CreateTreeParamToJson(this);
}
