import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/generated/l10n.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/models/params/trees/create_tree_params.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/ui/widgets/app_snackbar.dart';
import 'package:rxdart/rxdart.dart';
part 'update_tree_state.dart';

class UpdateTreeCubit extends Cubit<UpdateTreeState> {
  TreeRepository treeRepository;

  UpdateTreeCubit({
    required this.treeRepository,
  }) : super(UpdateTreeState());

  final showMessageController = PublishSubject<SnackBarMessage>();

  @override
  Future<void> close() {
    showMessageController.close();
    return super.close();
  }

  void changeName(String name) {
    emit(state.copyWith(name: name));
  }

  void changeDescription(String description) {
    emit(state.copyWith(description: description));
  }

  void updateTree(String? treeId) async {
    emit(state.copyWith(updateTreeStatus: LoadStatus.LOADING));
    try {
      final param =
          CreateTreeParam(name: state.name, description: state.description);
      print(param);
      final response =
          await treeRepository.updateTree(treeId: treeId, param: param);

      if (response != null) {
        emit(state.copyWith(updateTreeStatus: LoadStatus.SUCCESS));
      } else {
        emit(state.copyWith(updateTreeStatus: LoadStatus.FAILURE));
      }
    } catch (e) {
      emit(state.copyWith(updateTreeStatus: LoadStatus.FAILURE));
      return;
    }
  }

  Future<void> getTreeDetail(String treeId) async {
    emit(state.copyWith(loadStatus: LoadStatus.LOADING));
    try {
      final result = await treeRepository.getTreeById(treeId);

      emit(state.copyWith(
          loadStatus: LoadStatus.SUCCESS, treeData: result.data?.tree!));
    } catch (e) {
      emit(state.copyWith(loadStatus: LoadStatus.FAILURE));
    }
  }
}
