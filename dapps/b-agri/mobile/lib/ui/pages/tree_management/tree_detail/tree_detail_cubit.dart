import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/tree_repository.dart';

part 'tree_detail_state.dart';

class TreeDetailCubit extends Cubit<TreeDetailState> {
  TreeRepository treeRepository;
  TreeDetailCubit({required this.treeRepository}) : super(TreeDetailState());

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
