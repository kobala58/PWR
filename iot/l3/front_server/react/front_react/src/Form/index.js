import React from 'react';

export const Form = ({ onSubmit, data}) => {
  return (
    <form onSubmit={onSubmit}>
        <div className="form-group">
            <input
                type="text"
                className="form-control"
                id="svr_id"
                defaultValue={data[0]}
                disabled
            />
        </div>
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          type="text"
          className="form-control"
          id="name"
          defaultValue={data[1]}
        />
      </div>
      {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="method">METHOD</label>
            <input
                type="text"
                className="form-control"
                id="method"
                defaultValue={data[2]}
            />
        </div>
        {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="port">PORT</label>
            <input
                type="text"
                className="form-control"
                id="port"
                defaultValue={data[3]}
            />
        </div>
        {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="interval">INTERVAL</label>
            <input
                type="number"
                className="form-control"
                id="interval"
                defaultValue={data[4]}
            />
        </div>
        {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="source">SOURCE</label>
            <input
                type="text"
                className="form-control"
                id="source"
                defaultValue={data[5]}
            />
        </div>
        {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="channel">CHANNEL</label>
            <input
                type="text"
                className="form-control"
                id="channel"
                defaultValue={data[6]}
            />
        </div>
        {/*  DUPA */}
        <div className="form-group">
            <label htmlFor="server">SERVER</label>
            <input
                type="text"
                className="form-control"
                id="server"
                defaultValue={data[7]}
            />
        </div>
        {/*  DUPA */}
      <div className="form-group">
        <button className="form-control btn btn-primary" type="submit">
          Submit
        </button>
      </div>
    </form>
  );
};
export default Form;
