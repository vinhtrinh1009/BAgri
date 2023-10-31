import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/garden_repository.dart';
import 'package:flutter_base/ui/pages/auth/login/login_cubit.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';

import 'package:flutter_base/utils/logger.dart';
import 'package:rxdart/rxdart.dart';

part 'garden_list_state.dart';

class GardenListCubit extends Cubit<GardenListState> {
  GardenRepository? gardenRepository;

  GardenListCubit({this.gardenRepository}) : super(GardenListState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void fetchGardenList() async {
    emit(state.copyWith(getGardenStatus: LoginStatusBagri.LOADING));
    try {
      final response = await gardenRepository!.getGardenData();
      if (response != null) {
        emit(state.copyWith(
          getGardenStatus: LoginStatusBagri.SUCCESS,
          listGardenData: response.data!.gardens,
        ));
      } else {
        emit(state.copyWith(getGardenStatus: LoginStatusBagri.FAILURE));
      }
      emit(state.copyWith(getGardenStatus: LoginStatusBagri.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getGardenStatus: LoginStatusBagri.FAILURE));
    }
  }

  Future<void> deleteGarden(String? gardenId) async {
    emit(state.copyWith(deleteGardenStatus: LoadStatus.LOADING));
    try {
      final response = await gardenRepository!.deleteGarden(gardenId: gardenId);
      emit(state.copyWith(deleteGardenStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(deleteGardenStatus: LoadStatus.FAILURE));
      showMessageController.sink.add(SnackBarMessage(
        message: S.current.error_occurred,
        type: SnackBarType.ERROR,
      ));
      return;
    }
  }
}
