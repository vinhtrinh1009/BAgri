import 'package:json_annotation/json_annotation.dart';

part 'process_delete.g.dart';

@JsonSerializable()
class ProcessDeleteResponse {
  @JsonKey()
  String? status;
  @JsonKey()
  ProcessDeleteDataEntity? data;

  ProcessDeleteResponse({
    this.status,
    this.data,
  });

  ProcessDeleteResponse copyWith({
    String? status,
    ProcessDeleteDataEntity? data,
  }) {
    return ProcessDeleteResponse(
      status: status ?? this.status,
      data: data ?? this.data,
    );
  }

  factory ProcessDeleteResponse.fromJson(Map<String, dynamic> json) =>
      _$ProcessDeleteResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ProcessDeleteResponseToJson(this);
}

@JsonSerializable()
class ProcessDeleteDataEntity {
  @JsonKey()
  String? process_id;

  ProcessDeleteDataEntity({
    this.process_id,
  });

  ProcessDeleteDataEntity copyWith({
    String? process_id,
  }) {
    return ProcessDeleteDataEntity(
      process_id: process_id ?? this.process_id,
    );
  }

  factory ProcessDeleteDataEntity.fromJson(Map<String, dynamic> json) =>
      _$ProcessDeleteDataEntityFromJson(json);
  Map<String, dynamic> toJson() => _$ProcessDeleteDataEntityToJson(this);
}
