import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/garden/garden_detail.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/garden/create_garden_params.dart';
import 'package:flutter_base/repositories/garden_repository.dart';

import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:flutter_base/utils/logger.dart';
import 'package:rxdart/rxdart.dart';

part 'garden_update_state.dart';

class GardenUpdateCubit extends Cubit<GardenUpdateState> {
  GardenRepository? gardenRepository;

  GardenUpdateCubit({
    this.gardenRepository,
  }) : super(GardenUpdateState());

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

  void updateGarden(String? gardenId) async {
    emit(state.copyWith(editGardenStatus: LoadStatus.LOADING));
    try {
      final param = CreateGardenParam(
        name: state.name,
        area: state.area,
        manager_id: state.managerId,
      );
      final response = await gardenRepository!
          .updateGarden(gardenId: gardenId, param: param);

      if (response != null) {
        emit(state.copyWith(editGardenStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(editGardenStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      logger.e(e);
      emit(state.copyWith(editGardenStatus: LoadStatus.FAILURE));
      return;
    }
  }

  void fetchGardenDetail(String? gardenId) async {
    emit(state.copyWith(detailGardenStatus: LoadStatus.LOADING));
    try {
      final response =
          await gardenRepository!.getGardenDataById(gardenId: gardenId);
      if (response != null) {
        emit(state.copyWith(
          detailGardenStatus: LoadStatus.SUCCESS,
          gardenData: response.data!.garden,
          managerId: response.data!.garden!.manager!.manager_id,
        ));
      } else {
        emit(state.copyWith(detailGardenStatus: LoadStatus.FAILURE));
      }
    } catch (error) {
      emit(state.copyWith(detailGardenStatus: LoadStatus.FAILURE));
    }
  }
}
