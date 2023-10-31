import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:json_annotation/json_annotation.dart';

part 'tree_detail_response.g.dart';

@JsonSerializable()
class TreeDetailResponse {
  TreeEntity? tree;

  TreeDetailResponse({
    this.tree,
  });

  TreeDetailResponse copyWith({
    TreeEntity? tree,
  }) {
    return TreeDetailResponse(
      tree: tree ?? this.tree,
    );
  }

  factory TreeDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$TreeDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$TreeDetailResponseToJson(this);
}
