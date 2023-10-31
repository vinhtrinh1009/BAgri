import 'package:json_annotation/json_annotation.dart';

part 'list_tree_response.g.dart';

@JsonSerializable()
class ListTreeResponse {
  @JsonKey()
  String? status;
  @JsonKey()
  TreeDataEntity? data;

  ListTreeResponse({
    this.status,
    this.data,
  });

  ListTreeResponse copyWith({
    String? status,
    TreeDataEntity? data,
  }) {
    return ListTreeResponse(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory ListTreeResponse.fromJson(Map<String, dynamic> json) =>
      _$ListTreeResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ListTreeResponseToJson(this);
}

@JsonSerializable()
class TreeDataEntity {
  @JsonKey()
  List<TreeEntity>? trees;

  TreeDataEntity({
    this.trees,
  });

  TreeDataEntity copyWith({
    List<TreeEntity>? trees,
  }) {
    return TreeDataEntity(
      trees: trees ?? this.trees,
    );
  }

  factory TreeDataEntity.fromJson(Map<String, dynamic> json) =>
      _$TreeDataEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TreeDataEntityToJson(this);
}

@JsonSerializable()
class TreeEntity {
  String? id;
  @JsonKey()
  String? tree_id;
  @JsonKey()
  String? name;
  @JsonKey()
  String? description;

  factory TreeEntity.fromJson(Map<String, dynamic> json) =>
      _$TreeEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TreeEntityToJson(this);

  TreeEntity({
    this.id,
    this.tree_id,
    this.name,
    this.description,
  });

  TreeEntity copyWith({
    String? id,
    String? tree_id,
    String? name,
    String? description,
  }) {
    return TreeEntity(
      id: id ?? this.id,
      tree_id: tree_id ?? this.tree_id,
      name: name ?? this.name,
      description: description ?? this.description,
    );
  }
}
