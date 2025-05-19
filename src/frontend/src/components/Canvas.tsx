// @ts-nocheck
import React, { Component } from "react";

type PureCanvasProps = {
  contextRef: any;
  height: number;
  width: number;
};

type CanvasProps = {
  draw: Function;
  height: number;
  width: number;
};

class PureCanvas extends Component<PureCanvasProps> {
  shouldComponentUpdate({ width, height }: PureCanvasProps) {
    if (this.props.width !== width || this.props.height !== height) {
      return true;
    }
    return false;
  }

  getRef = (node: any) => {
    if (node) {
      this.props.contextRef(node.getContext("2d"));
    }

    return null;
  };

  render() {
    const { width, height } = this.props;

    return <canvas className="pure-canvas" width={width} height={height} ref={this.getRef} />;
  }
}

class Canvas extends Component<CanvasProps> {
  componentDidUpdate() {
    this.props.draw(this.ctx);
  }

  saveContext = (ctx) => {
    this.ctx = ctx;
  };

  render() {
    const { width, height } = this.props;

    return <PureCanvas contextRef={this.saveContext} width={width} height={height} />;
  }
}

export default Canvas;
