import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/garden/garden_detail.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';

import 'package:flutter_base/models/enums/load_status.dart';

import 'package:flutter_base/repositories/garden_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:rxdart/rxdart.dart';

part 'garden_detail_state.dart';

class GardenDetailCubit extends Cubit<GardenDetailState> {
  GardenRepository? gardenRepository;

  GardenDetailCubit({this.gardenRepository}) : super(GardenDetailState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void fetchGardenDetail(String? gardenId) async {
    emit(state.copyWith(getGardenStatus: LoadStatus.LOADING));
    try {
      final response =
          await gardenRepository!.getGardenDataById(gardenId: gardenId);
      if (response != null) {
        emit(state.copyWith(
          getGardenStatus: LoadStatus.SUCCESS,
          gardenData: response.data!.garden,
        ));
      } else {
        emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
      }
    } catch (error) {
      emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
    }
  }
}
