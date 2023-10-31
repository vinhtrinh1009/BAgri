import React from "react"
import PropTypes from "prop-types"
import { Pagination, PaginationItem, PaginationLink } from "reactstrap"

const CustomTablePagination = ({
    pagesCount, 
    currentPage, handleNextClick, handlePageClick, handlePreviousClick
}) => (
    <Pagination>
      <PaginationItem disabled={currentPage <= 1}>
        <PaginationLink onClick={handlePreviousClick} previous href="#" />
      </PaginationItem>
  
      {[...Array(pagesCount)].map((page, i) => (
        <PaginationItem active={i === currentPage-1} key={i+1}>
          <PaginationLink onClick={e => handlePageClick(e, i+1)} href="#">
            {i + 1}
          </PaginationLink>
        </PaginationItem>
      ))}
  
      <PaginationItem disabled={currentPage >= pagesCount}>
        <PaginationLink onClick={handleNextClick} next href="#" />
      </PaginationItem>
    </Pagination>
  );
CustomTablePagination.propTypes = {
    pagesCount: PropTypes.number.isRequired,
    currentPage: PropTypes.number.isRequired,
    handlePageClick: PropTypes.func.isRequired,
    handlePreviousClick: PropTypes.func.isRequired,
    handleNextClick: PropTypes.func.isRequired
}

export default CustomTablePagination