# coding: utf-8
"""
A* (A-star)経路探索プログラム
"""

from typing import List, Tuple, Optional, final


@final
class Node():
    """
    A node class for A* Path finding
    """

    def __init__(self, parent: Optional["Node"] = None, position: Optional[Tuple[int, int]] = None) -> None:
        self.parent = parent  # 親ノードの設定
        self.position = position  # (row, column)のタプル ※row：行、column：列

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: "Node") -> bool:
        # node 同士の比較演算子(==)を使用できるように
        return self.position == other.position


def astar(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze. nishioka
    """
    # maze: 迷路リスト、start:スタートポジション、end:ゴールポジション
    # ゴールまでの最短経路のリストを返す関数

    # Create start and end node
    # スタート、エンド（ゴール）ノードの初期化
    start_node = Node(None, start)  # 親ノードは無し
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list: List[Node] = []  # 経路候補を入れとくリスト
    closed_list: List[Node] = []  # 計算終わった用済みリスト
    # Add the start node
    # 経路候補にスタートノードを追加して計算スタート
    open_list.append(start_node)

    # Loop until you find the end
    infiniteFlag = 0
    while len(open_list) > 0:
        # 何故か無限ループする事がある為ループ上限設置
        infiniteFlag += 1
        if infiniteFlag > 1e3:
            print("A* infinite Loop!!")
            return None

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            # オープンリストの中でF値が一番小さいノードを選ぶ
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        # 一番小さいF値のノードをオープンリストから削除して、クローズリストに追加
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        # ゴールに到達してれば経路(Path)を表示して終了
        if current_node == end_node:
            path: List[Tuple[int, int]] = []
            current = current_node
            while current is not None:
                if current.position is not None:
                    path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        # ゴールに到達してなければ子ノードを生成
        children: List[Node] = []
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # 斜め移動ありの場合
        # 上下左右移動のみ (Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            if current_node.position is not None:
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                # 迷路内の移動に限る
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                # 移動できる位置に限る（障害物は移動できない）
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                # 移動できる位置のノードのみを生成
                new_node = Node(current_node, node_position)

                # Append
                # 子リストに追加
                children.append(new_node)

        # Loop through children
        # 各子ノードでG, H, Fを計算
        for child in children:

            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            if child.position is None or end_node.position is None:
                continue

            # Create the f, g, and h values
            # G は親ノード + 1
            child.g = current_node.g + 1
            # H は （現在位置 - エンド位置)の2乗
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            # F = G + H
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            # 子ノードをオープンリストに追加
            open_list.append(child)
