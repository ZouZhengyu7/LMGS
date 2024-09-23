import json
import copy
import os
import numpy as np
import open3d as o3d
import argparse


def EvaluateHisto(
        source,
        target,
        threshold,
        plot_stretch,
):
    print("[compute_point_cloud_to_point_cloud_distance]")
    distance1 = source.compute_point_cloud_distance(target)
    print("[compute_point_cloud_to_point_cloud_distance]")
    distance2 = target.compute_point_cloud_distance(source)

    [
        accuracy,
        Completion,
        precision,
        recall,
        fscore,
        edges_source,
        cum_source,
        edges_target,
        cum_target,
    ] = get_f1_score_histo2(threshold, plot_stretch, distance1,
                            distance2)

    return [
        accuracy,
        Completion,
        precision,
        recall,
        fscore,
        edges_source,
        cum_source,
        edges_target,
        cum_target,
    ]


def get_f1_score_histo2(threshold,
                        plot_stretch,
                        distance1,
                        distance2,
                        ):
    print("[get_f1_score_histo2]")
    dist_threshold = threshold
    accuracy = np.mean(distance1)
    Completion = np.mean(distance2)
    if len(distance1) and len(distance2):

        recall = float(sum(d < threshold for d in distance2)) / float(
            len(distance2))
        precision = float(sum(d < threshold for d in distance1)) / float(
            len(distance1))
        fscore = 2 * recall * precision / (recall + precision)
        num = len(distance1)
        bins = np.arange(0, dist_threshold * plot_stretch, dist_threshold / 100)
        hist, edges_source = np.histogram(distance1, bins)
        cum_source = np.cumsum(hist).astype(float) / num

        num = len(distance2)
        bins = np.arange(0, dist_threshold * plot_stretch, dist_threshold / 100)
        hist, edges_target = np.histogram(distance2, bins)
        cum_target = np.cumsum(hist).astype(float) / num

    else:
        precision = 0
        recall = 0
        fscore = 0
        edges_source = np.array([0])
        cum_source = np.array([0])
        edges_target = np.array([0])
        cum_target = np.array
    return accuracy, Completion, precision, recall, fscore, edges_source, cum_source, edges_target, cum_target


if __name__ == "__main__":
    source = o3d.io.read_point_cloud("/data1/zzy/zzy/LangSplat/scannet/scene0721_00/output/scene0721_00/point_cloud/iteration_30000/point_cloud.ply")
    target = o3d.io.read_point_cloud("/data1/zzy/zzy/LangSplat/scannet/scans/scene0721_00/scene0721_00_vh_clean_2.ply")
    threshold = 0.05
    plot_stretch = 1
    accuracy, Completion, precision, recall, fscore, edges_source, cum_source, edges_target, cum_target = EvaluateHisto(
        source,
        target,
        threshold,
        plot_stretch)
    print(f"{'Accuracy':<12} {'Completion':<15} {'Precision':<12} {'Recall':<8} {'F-Score':<8}")
    print(f"{accuracy:<12.4f} {Completion:<15.4f} {precision:<12.4f} {recall:<8.4f} {fscore:<8.4f}")