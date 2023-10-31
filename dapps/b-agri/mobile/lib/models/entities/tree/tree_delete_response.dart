import 'package:json_annotation/json_annotation.dart';

part 'tree_delete_response.g.dart';

@JsonSerializable()
class TreeDeleteResponse {
  @JsonKey()
  String? status;
  @JsonKey()
  TreeDeleteEntity? data;

  TreeDeleteResponse({
    this.status,
    this.data,
  });

  TreeDeleteResponse copyWith({
    String? status,
    TreeDeleteEntity? data,
  }) {
    return TreeDeleteResponse(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory TreeDeleteResponse.fromJson(Map<String, dynamic> json) =>
      _$TreeDeleteResponseFromJson(json);
  Map<String, dynamic> toJson() => _$TreeDeleteResponseToJson(this);
}

@JsonSerializable()
class TreeDeleteEntity {
  @JsonKey()
  String? tree_id;

  TreeDeleteEntity({
    this.tree_id,
  });

  TreeDeleteEntity copyWith({
    String? process_id,
  }) {
    return TreeDeleteEntity(
      tree_id: tree_id ?? this.tree_id,
    );
  }

  factory TreeDeleteEntity.fromJson(Map<String, dynamic> json) =>
      _$TreeDeleteEntityFromJson(json);
  Map<String, dynamic> toJson() => _$TreeDeleteEntityToJson(this);
}
