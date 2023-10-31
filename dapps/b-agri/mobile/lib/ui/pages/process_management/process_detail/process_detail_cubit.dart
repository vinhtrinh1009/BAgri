import 'package:bloc/bloc.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/process/process_detail.dart';
import 'package:flutter_base/models/entities/process/stage_entity.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:equatable/equatable.dart';

import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/response/object_response.dart';

part 'process_detail_state.dart';

class ProcessDetailCubit extends Cubit<ProcessDetailState> {
  ProcessRepository processRepository;
  ProcessDetailCubit({required this.processRepository})
      : super(ProcessDetailState(actionWithStepStatus: 0));

  Future<void> getProcessDetail(String processId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<ProcessDetailResponse> result =
          await processRepository.getProcessById(processId);
      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS,
          name: result.data?.process?.name!,
          trees: result.data?.process?.trees!,
          stages: result.data?.process?.stages!));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
