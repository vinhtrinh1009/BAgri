import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/response/object_response.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';
import 'package:flutter_base/utils/date_utils.dart' as date;

part 'employee_detail_state.dart';

class EmployeeDetailCubit extends Cubit<EmployeeDetailState> {
  FarmerRepository farmerRepository;
  EmployeeDetailCubit({required this.farmerRepository})
      : super(EmployeeDetailState(taskMapByDay: {}, chosenMonth: 1));

  void changeCurrentTaskList(int month) {
    if (month > 0 && month <= 12) {
      List<TaskEntity> currentTaskList = state.farmerDetail!.tasks!
          .where((element) => element.dateTime!.month == month)
          .toList();

      Map<int, List<TaskEntity>?> taskMapByDay = {};
      for (int i = 1; i <= 31; i++) taskMapByDay.addAll({i: []});

      for (TaskEntity e in currentTaskList) {
        int taskDay = e.dateTime!.day;
        taskMapByDay[taskDay]!.add(e);
      }

      emit(state.copyWith(taskMapByDay: taskMapByDay, chosenMonth: month));
    }
  }

  Future<void> getFarmerDetail(String farmerId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final ObjectResponse<FarmerDetailResponse> result =
          await farmerRepository.getFarmerById(farmerId);

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS, farmerDetail: result.data?.farmer));
      for (TaskEntity e in state.farmerDetail!.tasks!) {
        e.dateTime = date.DateUtils.fromStringFormatStrikeThrough(e.date!);
      }
      DateTime dateToday = DateTime.now();
      int currentMonth = dateToday.month;
      changeCurrentTaskList(currentMonth);
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
