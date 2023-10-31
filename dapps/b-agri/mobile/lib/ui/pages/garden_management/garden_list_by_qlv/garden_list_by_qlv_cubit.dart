import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/garden_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:rxdart/rxdart.dart';

part 'garden_list_by_qlv_state.dart';

class GardenListByQlvCubit extends Cubit<GardenListByQlvState> {
  GardenRepository? gardenRepository;

  GardenListByQlvCubit({this.gardenRepository}) : super(GardenListByQlvState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void fetchGardensByManagerId() async {
    emit(state.copyWith(getGardenStatus: LoadStatus.LOADING));
    try {
      final response = await gardenRepository!
          .getGardensByManagerId(GlobalData.instance.userEntity!.id!);
      if (response != null) {
        emit(state.copyWith(
          getGardenStatus: LoadStatus.SUCCESS,
          listGardenData: response.data!.gardens,
        ));
      } else {
        emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
      }
      emit(state.copyWith(getGardenStatus: LoadStatus.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
    }
  }
}
