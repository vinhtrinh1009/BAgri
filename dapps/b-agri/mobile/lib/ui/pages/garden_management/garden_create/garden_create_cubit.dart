import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/garden/create_garden_params.dart';
import 'package:flutter_base/repositories/garden_repository.dart';

import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:rxdart/rxdart.dart';

part 'garden_create_state.dart';

class GardenCreateCubit extends Cubit<GardenCreateState> {
  GardenRepository? gardenRepository;

  GardenCreateCubit({
    this.gardenRepository,
  }) : super(GardenCreateState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void changeName(String name) {
    emit(state.copyWith(name: name));
  }

  void changeArea(String area) {
    emit(state.copyWith(area: area));
  }

  void changeManagerId(String value) {
    emit(state.copyWith(managerId: value));
  }

  void createGarden() async {
    emit(state.copyWith(createGardenStatus: LoadStatus.LOADING));
    try {
      final param = CreateGardenParam(
        name: state.name,
        area: state.area,
        manager_id: state.managerId,
      );
      final response = await gardenRepository!.createGarden(param: param);

      if (response != null) {
        emit(state.copyWith(createGardenStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(createGardenStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      logger.e(e);
      emit(state.copyWith(createGardenStatus: LoadStatus.FAILURE));
      return;
    }
  }
}
