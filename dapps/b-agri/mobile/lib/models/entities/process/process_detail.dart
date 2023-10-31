import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:json_annotation/json_annotation.dart';

import 'list_process.dart';

part 'process_detail.g.dart';

@JsonSerializable()
class ProcessDetailResponse {
  ProcessEntity? process;

  factory ProcessDetailResponse.fromJson(Map<String, dynamic> json) =>
      _$ProcessDetailResponseFromJson(json);
  Map<String, dynamic> toJson() => _$ProcessDetailResponseToJson(this);

  ProcessDetailResponse({
    this.process,
  });

  ProcessDetailResponse copyWith({
    ProcessEntity? process,
  }) {
    return ProcessDetailResponse(
      process: process ?? this.process,
    );
  }
}

// @JsonSerializable()
// class StageEntity {
//   String? name;
//   dynamic duration;
//   List<TaskEntity>? steps;
//
//   factory StageEntity.fromJson(Map<String, dynamic> json) =>
//       _$StageEntityFromJson(json);
//   Map<String, dynamic> toJson() => _$StageEntityToJson(this);
//
//   StageEntity({
//     this.name,
//     this.duration,
//     this.steps,
//   });
//
//   StageEntity copyWith({
//     String? name,
//     dynamic duration,
//     List<TaskEntity>? steps,
//   }) {
//     return StageEntity(
//       name: name ?? this.name,
//       duration: duration ?? this.duration,
//       steps: steps ?? this.steps,
//     );
//   }
// }
